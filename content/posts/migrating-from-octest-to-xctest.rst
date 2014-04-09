Migrating from OCUnit to XCTest
###############################

:date: 2014-04-09
:tags: xcode, tdd, xctest, ocunit, sentesting, objective-c

.. |br| raw:: html

    <br />

You might think you were in luck when Xcode offered you an option to migrate to
XCTest, but shortly after trying you will discover that this isn't a true
migration. Xcode will only migrate your code, it will not update your project
to be testable with XCTest. There are still some steps left and unfortunately
Apple have not shared any documentation on how to do this.

|br|

.. image:: /static/images/migrate-xctest/convert.png
    :width: 420px
    :height: 129px
    :align: center

|br|

You can follow these steps to migrate your project to XCTest once you've
migrated the code with the automatic converter:

1. Change the `Wrapper Extension` your project's test target in build
   settings from `ocunit` to `xctest`.

.. container:: image-zoom

    .. image:: /static/images/migrate-xctest/wrapper-extension.png
        :width: 636px
        :height: 319px
        :align: center

2. Remove the OCUnit `Run Script` build phase from your project's test target.

.. container:: image-zoom

    .. image:: /static/images/migrate-xctest/run-script-build-phase.png
        :width: 636px
        :height: 319px
        :align: center

3. Replace `SenTestingKit` framework with `XCTest` inside the test target's
   link with libraries build phase.

.. container:: image-zoom

    .. image:: /static/images/migrate-xctest/frameworks.png
        :width: 636px
        :height: 319px
        :align: center

4. For iOS, you may need to add the SDK's developer frameworks so the linker
   can find the XCTest framework for iOS when building the project.

   You will need to add `$(SDKROOT)/Developer/Library/Frameworks` to the
   framework search paths for the test target.

.. container:: image-zoom

    .. image:: /static/images/migrate-xctest/framework-search.png
        :width: 676px
        :height: 316px
        :align: center

Kiwi
----

If you are using Kiwi, be sure switch to the `XCTest` pod.

.. code-block:: ruby

    pod 'Kiwi/XCTest'

