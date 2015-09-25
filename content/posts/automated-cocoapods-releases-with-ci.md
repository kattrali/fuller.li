Title: Automated CocoaPod releases with CI
Slug: automated-cocoapods-releases-with-ci
Category: CocoaPods
Tags: CocoaPods, CI
Date: 2015-09-25

Using continuous integration (CI), we can automate releasing our
[CocoaPods](https://cocoapods.org/) to trunk. When someone tags a new release
and runs `git push`, CI will publish the pod to CocoaPods trunk.

This guide walks you though settings this up on both
[Circle CI](https://circleci.com) and [Travis CI](https://travis-ci.org). If
you are not using these CI providers, you should be able to follow a similar
technique.

### CocoaPods trunk Access Token

To release new or updates to existing pods you will need an access token
for trunk. This is normally created using the `pod trunk register` command.

We're going to use this command to generate a unique token for our CI server to
perform release. Using the following:

```shell
$ pod trunk register kyle@fuller.li --description='CI Automation'
[!] Please verify the session by clicking the link in the verification email that has been sent to kyle@fuller.li
```

**NOTE**: *Remember to change my email address for the email address you use
with CocoaPods.*

The next step will be to go to your email and "verify" the session by following
the link in your email.

> Hi Kyle,
>
> Please confirm your CocoaPods session by clicking the following link:
> `https://trunk.cocoapods.org/sessions/verify/uniquehash`

Once your session is verified, we can then grab the access token from CocoaPods to use in CI . CocoaPods stores the access token in the standard `~/.netrc` file.

We can pull this out using the following:

```shell
$ grep -A2 'trunk.cocoapods.org' ~/.netrc
machine trunk.cocoapods.org
  login kyle@fuller.li
  password ef9bb4c41a4459ba92645a85b3c9cd88
```

You can see our token is `ef9bb4c41a4459ba92645a85b3c9cd88`, we now will need
to configure our CI server and set the environmental variable
`COCOAPODS_TRUNK_TOKEN` with the value of our token.

**IMPORTANT**: *Once you have an access token for CI, you should
run `pod trunk register` again so you are locally using a separate token from the CI service.*

#### Circle CI

On Circle CI, the access token can be configured in the settings for your repository on
their website.

![Circle CI environmental variables](/images/cocoapods-ci/circleci-env.png)

#### Travis CI

Like Circle CI, you can also add the access token for CocoaPods trunk in the settings for your repository like follows:

![Travis CI environmental variables](/images/cocoapods-ci/travisci-env.png)

**IMPORTANT**: *Ensure that `Display value in build log` is not enabled.*

You can also use the `travis` CLI tool to [encrypt environmental variables in your `.travis.yml` file](http://docs.travis-ci.com/user/encryption-keys/).

### Running `pod trunk push` when new releases are tagged

The next step is to configure our CI process to push our pod when a new release
is tagged.

#### Circle CI

For Circle CI, we can add a `deployment` section to run the `pod trunk push` command on new tags.

```yaml
machine:
  xcode:
    version: "7.0"

deployment:
  release:
    tag: /.*/
    commands:
      - pod trunk push
```

#### Travis CI

Similarly on Travis CI, we can add a `deploy` section to run a custom script
`scripts/push.sh` on new tags.

```yaml
language: objective-c
osx_image: xcode7
deploy:
  provider: script
  script: ./scripts/push.sh
  on:
    tags: true
```

You will need to create a `scripts/push.sh` file in your repository and commit
it so that Travis CI will configure rvm (ruby version manager), and then
run `pod trunk push` on deployment.

```bash
#!/usr/bin/env bash

source ~/.rvm/scripts/rvm
rvm use default
pod trunk push
```

### Pushing your Pod

That's it, now when you push new versions to your CI server they will automatically be released to CocoaPods trunk!

```shell
$ edit Stencil.podspec
# Update the version in the podspec
$ git add Stencil.podspec
$ git commit -m 'Release 1.0.0'
$ git tag 1.0.0
$ git push origin master --tags
```

Examples:

- [Stencil](https://github.com/kylef/Stencil/blob/0.3.0/circle.yml#L10) uses Circle CI for deployment
- [Commander](https://github.com/kylef/Commander/blob/0.2.1/.travis.yml#L9) uses Travis CI for deployment

#### Note on Security

It's important to note that we've uploaded an access token to our CI server.
Using this token it's possible to publish new, or update your pods.
Therefore it's extremely important to keep this token private and do not
share it with anyone.

In the event that your trunk session has been compromised, you can
invalidate any other sessions using the following:

```shell
$ pod trunk me clean-sessions --all
```

