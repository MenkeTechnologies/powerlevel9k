#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"

  # Test specific settings
  OLD_DEFAULT_USER=$DEFAULT_USER
  unset DEFAULT_USER
}

function tearDown() {
  # Restore old variables
  [[ -n "$OLD_DEFAULT_USER" ]] && DEFAULT_USER=$OLD_DEFAULT_USER

  return 0
}

function testContextSegmentDoesNotGetRenderedWithDefaultUser() {
    local DEFAULT_USER=$(whoami)
    local POWERLEVEL9K_CUSTOM_WORLD='echo world'
    local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context custom_world)

    # Load Powerlevel9k
    source powerlevel9k.zsh-theme

    assertEquals "%K{015} %F{000}world %k%F{015}%f " "$(build_left_prompt)"
}

function testContextSegmentDoesGetRenderedWhenSshConnectionIsOpen() {
    function sudo() {
        return 0
    }
    local SSH_CLIENT="putty"
    local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)

    # Load Powerlevel9k
    source powerlevel9k.zsh-theme

    assertEquals "%K{000} %F{011}%n@%m %k%F{000}%f " "$(build_left_prompt)"

    unfunction sudo
}

function testContextSegmentWithForeignUser() {
    function sudo() {
        return 0
    }
    local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)

    # Load Powerlevel9k
    source powerlevel9k.zsh-theme

    assertEquals "%K{000} %F{011}%n@%m %k%F{000}%f " "$(build_left_prompt)"

    unfunction sudo
}

# TODO: How to test root?
function testContextSegmentWithRootUser() {
    startSkipping # Skip test
    local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)

    # Load Powerlevel9k
    source powerlevel9k.zsh-theme

    assertEquals "%K{000} %F{011}%n@%m %k%F{000}%f " "$(build_left_prompt)"
}

function testOverridingContextTemplate() {
    local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)
    local POWERLEVEL9K_CONTEXT_TEMPLATE=xx

    # Load Powerlevel9k
    source powerlevel9k.zsh-theme

    assertEquals "%K{000} %F{011}xx %k%F{000}%f " "$(build_left_prompt)"
}

function testContextSegmentIsShownIfDefaultUserIsSetWhenForced() {
    local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)
    local POWERLEVEL9K_ALWAYS_SHOW_CONTEXT=true
    local DEFAULT_USER=$(whoami)

    # Load Powerlevel9k
    source powerlevel9k.zsh-theme

    assertEquals "%K{000} %F{011}%n@%m %k%F{000}%f " "$(build_left_prompt)"
}

function testContextSegmentIsShownIfForced() {
    local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context)
    local POWERLEVEL9K_ALWAYS_SHOW_USER=true
    local DEFAULT_USER=$(whoami)

    # Load Powerlevel9k
    source powerlevel9k.zsh-theme

    assertEquals "%K{000} %F{011}$(whoami) %k%F{000}%f " "$(build_left_prompt)"
}

source shunit2/shunit2