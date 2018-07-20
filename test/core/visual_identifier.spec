#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme
  source functions/*
}

function testOverwritingIconsWork() {
  local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
  POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(custom_world1)
  local POWERLEVEL9K_CUSTOM_WORLD1='echo world1'
  local POWERLEVEL9K_CUSTOM_WORLD1_ICON='icon-here'

  assertEquals "%K{white} %F{black%}icon-here %f%F{black}world1 %k%F{white}%f " "$(build_left_prompt)"
}

function testVisualIdentifierAppearsBeforeSegmentContentOnLeftSegments() {
  local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
  POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(custom_world1)
  local POWERLEVEL9K_CUSTOM_WORLD1='echo world1'
  local POWERLEVEL9K_CUSTOM_WORLD1_ICON='icon-here'

  assertEquals "%K{white} %F{black%}icon-here %f%F{black}world1 %k%F{white}%f " "$(build_left_prompt)"
}

function testVisualIdentifierAppearsAfterSegmentContentOnRightSegments() {
  local -a POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS
  POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(custom_world1)
  local POWERLEVEL9K_CUSTOM_WORLD1='echo world1'
  local POWERLEVEL9K_CUSTOM_WORLD1_ICON='icon-here'

  assertEquals "%F{white}%f%K{white}%F{black} world1%F{black%} icon-here%f%E" "$(build_right_prompt)"
}

function testVisualIdentifierPrintsNothingIfNotAvailable() {
  local -a POWERLEVEL9K_LEFT_PROMPT_ELEMENTS
  POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(custom_world1)
  local POWERLEVEL9K_CUSTOM_WORLD1='echo world1'

  assertEquals "%K{white} %F{black}world1 %k%F{white}%f " "$(build_left_prompt)"
}

source shunit2/source/2.1/src/shunit2