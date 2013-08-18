Versioning with Xcode and git
#############################

:date: 18/08/2013
:tags: Xcode, Objective-C

Wouldn't it be great if your iOS or OS X projects just take their version and
build number automatically from git? Well, it can!

Using a script in your build phase, you can run a shell to determine the
version number and inject this into the `Info.plist` of a build. It will
never modify your local project, just the created build.

.. code-block:: bash

    GIT_RELEASE_VERSION=$(git describe --tags --always --dirty)
    COMMITS=$(git rev-list HEAD | wc -l)
    COMMITS=$(($COMMITS))
    defaults write "${BUILT_PRODUCTS_DIR}/${INFOPLIST_PATH%.*}" "CFBundleShortVersionString" "${GIT_RELEASE_VERSION#*v}"
    defaults write "${BUILT_PRODUCTS_DIR}/${INFOPLIST_PATH%.*}" "CFBundleVersion" "${COMMITS}"

Once you have the build phase in place, your version number will be created
using the last git tag. If the build was generated right after creating a git
tag. Then the version will simply be the tag. If you have made a few commits
after tagging, then you will will get a version number suffixed with the amount
of commits since the last tag, and the current hash. The hash is important
because it allows you to get back to that commit and find the exact code base
from a version number.

I always create a new tag before releasing to the app store, so any released
applications will have a nice clean version number such as `1.0` or `1.2`. Any
pre-release builds will often include the previous tag along with how many
commits since this tag and the hash. These builds should look something like
`1.2-52-g8bdae1d`.

Adding the build phase to your project
--------------------------------------

To add this build phase to your Xcode project, go into your project file and
select the target you want to use. Then hit **Editor > Add Build Phase > Add
Run Script Build Phase**. Next, you will need to copy the above shell script
into the newly created build phase.

Afterwards, your project should contain a phase looking like this:

.. image:: /static/images/versioning-with-xcode.png
    :width: 671px
    :height: 563px
    :align: center

There are two components to versioning. Firstly there is the version string
which was described above. There is also a version number, this has to be a
number which is always incremented on any build going to the app store.

If you have uncommitted files, the version string will be suffixed by `-dirty`
to indicate it's dirty. You can disable this by removing `--dirty` from the
first line in the build phase. However I find it useful to know if the build
has uncommitted changes.

To conclude, here are some possible examples:

* `1.0` from a build directly from a tag.
* `1.0-dirty` from a build directly from a tag, with uncommitted code.
* `1.0-2-g8bdae1d` from a build on commit `g8bdae` which is 2 commits in
  front of the `1.0` tag.
* `g8bdae1d` which would indicate that there are no tags.
