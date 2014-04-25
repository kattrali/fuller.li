Memory Management with ARC
##########################

:author: kylef
:date: 2013-10-24
:slug: memory-management-arc
:tags: ARC, Memory Management, Objective-C, iOS, OS X

This blog post accompanies a talk I recently gave at NSLondon, you can find the
slides for this talk `here <https://speakerdeck.com/kylef/memory-management>`_.
There will also be a video version of this out shortly, I will post a link once
it's out on my `Twitter <https://twitter.com/kylefuller>`_.

ARC is a very powerful feature introduced in Xcode in 4.0, along with various
run-time enhancements. With the introduction of ARC, a lot has changed under the
hood. The Objective-C run-time has a completely new interface for using many of the
old concepts such as autorelease pools. There is also a new interface for
retaining and releasing objects.

This post will briefly explain these concepts, along with how they work in the
runtime. It will include any common mistakes such as retain cycles, the dealloc
problem and `copy` vs `strong` with blocks.

Retainable Object Pointers
==========================

Automatic Reference Counting (ARC) is a tool for managing retainable object
pointers. This is any kind of pointer to an object which can handle the
Objective-C machinery for sending the `retain`, `release` and `autorelease`
messages.

These messages are not sent in the way they would have been done pre-ARC, but
instead using the `objc_retain`, `objc_release` and `objc_retainAutorelease`
functions.

Retainable types include `id`, `Class` and `NSObject`. Along with
`__attribute__((NSObject))`.

`__attribute__((NSObject))` is an attribute which allows you to declare that a
typedef can support memory management by ARC. That the `objc_retain`,
`objc_release` and `objc_retainAutorelease` function is supported with this
type and that it can retain and release memory as expected.

`dispatch_queue_t` is a perfect example of this. Starting in iOS 6 and OS X
10.8, this type (and many other types) support memory management by ARC.
Therefore you can use use these types with the strong property referencing.

.. code-block:: objective-c

    @property (nonatomic, strong) dispatch_queue_t completionBlock;


Ownership Qualification
=======================

What gives ARC it's immense power, is the fact that you can mark different
pieces of memory with qualifiers to indicate how it should be handled.
Weather it be strongly holding them with the `__strong` qualifier or not
doing any management at all with the `__unsafe_unretained` qualifier.

__unsafe_unretained
-------------------

__unsafe_unretained is by far the most simple. It basically means that no
memory management will be done. It can be used for both objects and scalar
types such as `int` and `BOOL`.

__strong
--------

The strong qualifier will **strongly** hold an object. It does so by
retaining an object when one is set to a strong pointer. When this pointer is
set to nil, the object is released.

For example, the following two piece of code will do nearly identical things.

.. code-block:: objective-c

    // Without ARC
    - (void)setName:(NSString *)name {
        [_name release];
        _name = name;
        [_name retain];
    }

    // With ARC
    - (void)setName:(NSString *)name {
        _name = name;
    }

.. **

__weak
------

Weak is an interesting qualification. It allows you to reference an
object, when the object is deallocated the pointer will become nil.
Instead of retaining an object, the object's retain count will not change
with weak referencing.

Because weak objects can be released at any point of time, it's often
important to create a strong reference to it. This allows you to keep it
alive while it's in use.

Most of the work for weak referencing is done in the new run-time support
in Objective-C, introduced in LLVM along with ARC.

When setting a weak pointer, ARC will call `id objc_storeWeak(id *object, id
value)` which simply adds the pointer (object) to the `value` object's table of
weak references.

Now, when the object `value` is deallocated, it will iterate over every object
in the weak referencing table and set those weak references to nil.

Alternatively, the `objc_destroyWeak(id *object)` function is used to delete
this pointer from the object's weak reference table. This is normally called
from an object's dealloc.

Because weak has to maintain this table of references, it adds the necessary
overhead to do this. I have done some testing and it shows that weak referencing
can take over three times as long as the normal strong referencing.

objc_arc_weak_unavailable
~~~~~~~~~~~~~~~~~~~~~~~~~

Using the `objc_arc_weak_unavailable` attribute, you can mark an object so that
it cannot be used with the weak qualification. This may be handy for types
which use `__attribute__((NSObject))`.

__autoreleasing
---------------

Autoreleasing has been around for a while, however it has changed a lot with
the introduction of ARC. You can no longer use the `NSAutoreleasePool` class.

Instead, you can use the `objc_autoreleaseReturnValue(id value)` function to
autorelease an object. This will retain the object and then return it. While
it will also add it to the current release pool.

To drain the release pool the `objc_autoreleasePoolPop(void *pool)` function is called.

Blocks
======

I often see this question of `strong` vs `copy` for blocks and there is a lot
of confusion about what you should be using.

In Apple's transitioning to ARC guide, they mention this:

    Blocks "just work" when you pass blocks up the stack in ARC mode, such as
    in a return. You don’t have to call Block Copy any more. You still need
    to use `[^{} copy]` when passing "down" the stack into `arrayWithObjects:`
    and other methods that do a retain.

Blocks will be stored in the current stack, this means they are available in
the local scope. If you use them outside, you must make a copy of the block.
Otherwise ARC will retain these objects, and then when they go out of memory
you'll have a pointer to something that has been released.

This is not normally a problem, often you will want to run a block from the
current stack. However, sometimes you want to use them with properties and that
might mean you will want to use it outside of the current stack. Therefore it
is important to take a copy.

.. code-block:: objective-c

    @property (nonatomic, copy) dispatch_block_t block;

You might also want to convert a block type to `id` for use in an array or
something similar. You will also need to make a copy, for example:

.. code-block:: objective-c

    dispatch_block_t block = ^{
        NSLog(@"Hello World!");
    };

    NSArray *blocks = [[NSArray alloc] initWithObject:[block copy]];

.. **

Retain Cycle
============

A retain cycle is an issue where you have a retain-able object which
indirectly has a strong reference to itself. Usually using another block or
object.

For example:

.. code-block:: objective-c

    - (void)startOperation {
        NSOperation *operation = [[NSOperation alloc] init];

        [operation setCompletionBlock:^{
            NSLog(@"Completion for %@", operation);
        }];
    }

.. **

The above example shows a completion block which has a strong reference to the
operation. For the lifetime of this block, the operation will stay alive.

You will notice, that the operation strongly holds onto the completion block
too. Which means that the completion block will be alive for the lifespan of
the operation.

It's clear we have a problem, ARC won't ever be able to release this object.

The solution would be to use a weak reference to the operation:

.. code-block:: objective-c

    - (void)startOperation {
        NSOperation *operation = [[NSOperation alloc] init];
        __weak NSOperation *weakOperation = operation;

        [operation setCompletionBlock:^{
            NSLog(@"Completion for %@", weakOperation);
        }];
    }

.. **

The Deallocation Problem
=========================

One of the hardest problems with ARC comes to deallocating your objects safely.
It's common to retain objects in the background. When a secondary thread has
the last reference to an object. It will be responsible for deallocating the
object.

When this object is one of the many UIKit objects, such as a view controller.
This can cause a real problem if it's deallocated in the background. It's often
very difficult to both debug, and to reproduce this issue since it's a race
condition.

To help prevent this problem, you should always use __weak when referencing
UIKit objects in the background.

Apple have described this problem on
`TN2109 <https://developer.apple.com/library/ios/technotes/tn2109/_index.html>`__.

CoreFoundation
==============

CoreFoundation objects are not subject to ARC. You still have to maintain these
objects like you have done in the past.

.. code-block:: objective-c

    CGRelease(stringRef);

Remember to be careful when using CG objects, especially if they are not owned
by you. In the following example, we are retrieving a CGColor reference
from UIColor. UIColor owns this reference, and is responsible for memory
management.

.. code-block:: objective-c

    UIColor *whiteColor = [UIColor whiteColor];
    CGColorRef whiteRef = [whiteColor CGColor];

    // Crash when using whiteRef

.. **

This example will result in ARC releasing UIColor after line 2 because it is no
longer used. The whiteRef will now be a pointer to a piece of memory which may
have been released at this stage.

Instead you should use the following code, which will retain this reference for
ourself.

.. code-block:: objective-c

    UIColor *whiteColor = [UIColor whiteColor];
    CGColorRef whiteRef = CGRetain([whiteColor CGColor]);

    // Use whiteRef

    CGRelease(whiteRef);

.. **

Exceptions
==========

By default, exceptions are not ARC safe. Conventionally, an exception in
Objective-C represents an unrecoverable error. So ARC not being exception safe
is perfectly fine and acceptable behaviour. However, there is still a way to
enable it using the `-fobjc-arc-exceptions` compiler flag.

You can enable a compiler option to handle exceptions properly with ARC.
But you probably shouldn't do this!

