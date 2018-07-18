#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme
}

function mockRust() {
  echo 'rustc  0.4.1a-alpha'
}

function testSshSegmentPrintsNothingIfNoSshConnection() {
  local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(ssh custom_world)
  local POWERLEVEL9K_CUSTOM_WORLD='echo "world"'
  local POWERLEVEL9K_SSH_ICON="ssh-icon"
  # Weak test: Emulate No SSH connection by unsetting
  # $SSH_CLIENT and $SSH_TTY
  unset SSH_CLIENT
  unset SSH_TTY

  assertEquals "%K{white} %F{black}world %k%F{white}%f " "$(build_left_prompt)"
}

function testSshSegmentWorksIfOnlySshClientIsSet() {
  local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(ssh)
  local POWERLEVEL9K_SSH_ICON="ssh-icon"
  # Weak test: Emulate No SSH connection by unsetting
  # $SSH_CLIENT and $SSH_TTY
  SSH_CLIENT='ssh-client'
  unset SSH_TTY

  assertEquals "%K{black} %F{yellow%}ssh-icon%f %k%F{black}%f " "$(build_left_prompt)"

  unset SSH_CLIENT
}

function testSshSegmentWorksIfOnlySshTtyIsSet() {
  local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(ssh)
  local POWERLEVEL9K_SSH_ICON="ssh-icon"
  # Weak test: Emulate No SSH connection by unsetting
  # $SSH_CLIENT and $SSH_TTY
  SSH_TTY='ssh-tty'
  unset SSH_CLIENT

  assertEquals "%K{black} %F{yellow%}ssh-icon%f %k%F{black}%f " "$(build_left_prompt)"

  unset SSH_TTY
}

function testSshSegmentWorksIfAllNecessaryVariablesAreSet() {
  local POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(ssh)
  local POWERLEVEL9K_SSH_ICON="ssh-icon"
  # Weak test: Emulate No SSH connection by unsetting
  # $SSH_CLIENT and $SSH_TTY
  SSH_CLIENT='ssh-client'
  SSH_TTY='ssh-tty'

  assertEquals "%K{black} %F{yellow%}ssh-icon%f %k%F{black}%f " "$(build_left_prompt)"

  unset SSH_TTY
  unset SSH_CLIENT
}

source shunit2/source/2.1/src/shunit2