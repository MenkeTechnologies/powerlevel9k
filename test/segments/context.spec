#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  # Test specific settings
  OLD_DEFAULT_USER=$DEFAULT_USER
  unset DEFAULT_USER
}

function tearDown() {
  # Restore old variables
  [[ -n "$OLD_DEFAULT_USER" ]] && DEFAULT_USER=$OLD_DEFAULT_USER
}

function testContextSegmentDoesNotGetRenderedWithDefaultUser() {
    local DEFAULT_USER=$(whoami)
    local POWERLEVEL9K_CUSTOM_WORLD='echo world'
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context custom_world)

    assertEquals "%K{white} %F{black}world %k%F{white}%f " "$(build_left_prompt)"
}

function testContextSegmentDoesGetRenderedWhenSshConnectionIsOpen() {
    local SSH_CLIENT="putty"
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)

    assertEquals "%K{black} %F{yellow}%n@%m %k%F{black}%f " "$(build_left_prompt)"
}

function testContextSegmentWithForeignUser() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)

    assertEquals "%K{black} %F{yellow}%n@%m %k%F{black}%f " "$(build_left_prompt)"
}

# TODO: How to test root?
function testContextSegmentWithRootUser() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)
    startSkipping # Skip test

    assertEquals "%K{black} %F{yellow}%n@%m %k%F{black}%f " "$(build_left_prompt)"
}

function testOverridingContextTemplate() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)
    local POWERLEVEL9K_CONTEXT_TEMPLATE=xx

    assertEquals "%K{black} %F{yellow}xx %k%F{black}%f " "$(build_left_prompt)"
}

function testContextSegmentIsShownIfDefaultUserIsSetWhenForced() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)
    local POWERLEVEL9K_ALWAYS_SHOW_CONTEXT=true
    local DEFAULT_USER=$(whoami)

    assertEquals "%K{black} %F{yellow}%n@%m %k%F{black}%f " "$(build_left_prompt)"
}

function testContextSegmentIsShownIfForced() {
    local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)
    local POWERLEVEL9K_ALWAYS_SHOW_USER=true
    local DEFAULT_USER=$(whoami)

    assertEquals "%K{black} %F{yellow}$(whoami) %k%F{black}%f " "$(build_left_prompt)"
}

source shunit2/source/2.1/src/shunit2