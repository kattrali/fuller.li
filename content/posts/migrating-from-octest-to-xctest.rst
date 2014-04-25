Migrating from OCUnit to XCTest
###############################

:date: 2014-04-09
:tags: Xcode, tdd, XCTest, OCUnit, SenTesting, Objective-C

.. |br| raw:: html

    <br />

You might think you were in luck when Xcode offered you an option to migrate to
XCTest, but shortly after trying you will discover that this isn't a true
migration. Xcode will only migrate your code, it will not update your project
to be testable with XCTest. There are still some steps left and unfortunately
Apple have not shared any documentation on how to do this.

.. note:: I have later discovered that it does work as expected, but only if
  you run the conversion from a project directly. If you try running the
  conversion from a workspace you will get the problems mentioned above. I
  have filed this as rdar://16581037 so Apple can fix this in the future. For
  now, you'll need to follow the below steps.

|br|

.. image:: /images/migrate-xctest/convert.png
    :alt: OCUnit is deprecated, Convert to XCTest
    :width: 420px
    :height: 129px
    :align: center

|br|

You can follow these steps to migrate your project to XCTest once you've
migrated the code with the automatic converter:

---

1. Change the `Wrapper Extension` your project's test target in build
   settings from `ocunit` to `xctest`.

.. container:: image-zoom

    .. image:: /images/migrate-xctest/wrapper-extension.png
        :alt: Test Target's Wrapper Extension
        :width: 636px
        :height: 319px
        :align: center

2. This is the scary part, you are going to need to manually edit your Xcode
   project by hand and replace the product type for your test target. Firstly,
   close Xcode and then open the project's `project.pbxproj` in your favourite
   text editor and search for the product type. You will need to change it from
   `com.apple.product-type.bundle` to `com.apple.product-type.bundle.unit-test`.

.. code-block:: diff

     productReference = 77DC06B215702EDB0001EF8C /* PalaverTests.xctest */
    -productType = "com.apple.product-type.bundle";
    +productType = "com.apple.product-type.bundle.unit-test";


3. Remove the OCUnit `Run Script` build phase from your project's test target.

.. container:: image-zoom

    .. image:: /images/migrate-xctest/run-script-build-phase.png
        :alt: OCUnit Run Script Build Phase
        :width: 636px
        :height: 319px
        :align: center

4. Replace `SenTestingKit` framework with `XCTest` inside the test target's
   link with libraries build phase. Even better, you can `clean up your project
   <http://tonyarnold.com/2014/04/10/clean-up-your-projects-with-xcode-5.html>`_
   by enabling modules instead of adding XCTest.

.. container:: image-zoom

    .. image:: /images/migrate-xctest/frameworks.png
        :alt: Replacing SenTestkingKit for XCTest framework
        :width: 636px
        :height: 319px
        :align: center

5. For iOS, you may need to add the SDK's developer frameworks so the linker
   can find the XCTest framework for iOS when building the project.

   You will need to add `$(SDKROOT)/Developer/Library/Frameworks` to the
   framework search paths for the test target.

.. container:: image-zoom

    .. image:: /images/migrate-xctest/framework-search.png
        :alt: Adding Developer frameworks to search paths
        :width: 676px
        :height: 316px
        :align: center

Kiwi
----

If you are using Kiwi, be sure switch to the `XCTest` pod.

.. code-block:: ruby

    pod 'Kiwi/XCTest'

