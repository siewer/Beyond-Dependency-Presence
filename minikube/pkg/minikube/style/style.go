/*
Copyright 2019 The Kubernetes Authors All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package style

import (
	"strings"
)

var (
	// LowBullet is a bullet-point prefix for Low-fi mode
	LowBullet = "* "
	// LowIndent is an indented prefix for Low-fi mode
	LowIndent = "  "
	// LowIndentBullet is an indented bullet-point prefix for Low-fi mode
	LowIndentBullet = "  - "
	// LowWarning is a warning prefix for Low-fi mode
	LowWarning = "! "
	// LowError is an error prefix for Low-fi mode
	LowError = "X "
	// Indented is how far to indent unstyled text
	Indented = "    "
)

// Options describes how to stylize a message.
type Options struct {
	// Prefix is a string to place in the beginning of a message
	Prefix string
	// LowPrefix is the 7-bit compatible prefix we fallback to for less-awesome terminals
	LowPrefix string
	// ShouldSpin is a character to place at ending of message
	ShouldSpin    bool
	HideAfterSpin bool // Hide the prefix after spinning
}

// SpinnerCharacter is which of the spinner.CharSets to use
const SpinnerCharacter = 9

// SpinnerSubStepCharacter is Character to use for sub-steps in a spinner (it looks like a progress bar)
const SpinnerSubStepCharacter = 40

// Config is a map of style name to style struct
// For consistency, ensure that emojis added render with the same width across platforms.
var Config = map[Enum]Options{
	Celebration:        {Prefix: "🎉  "},
	Check:              {Prefix: "✅  "},
	Command:            {Prefix: "    ▪ ", LowPrefix: LowIndentBullet},
	Confused:           {Prefix: "😕  "},
	Deleted:            {Prefix: "💀  "},
	Documentation:      {Prefix: "📘  "},
	Empty:              {Prefix: "", LowPrefix: ""},
	Happy:              {Prefix: "😄  "},
	Issue:              {Prefix: "    ▪ ", LowPrefix: LowIndentBullet},
	Indent:             {Prefix: "    ", LowPrefix: LowIndent},
	Issues:             {Prefix: "🍿  "},
	Launch:             {Prefix: "🚀  "},
	LogEntry:           {Prefix: "    "}, // Indent
	New:                {Prefix: "🆕  "},
	Notice:             {Prefix: "📌  "},
	Option:             {Prefix: "    ▪ ", LowPrefix: LowIndentBullet},
	Pause:              {Prefix: "⏸️  "},
	Provisioning:       {Prefix: "🌱  "},
	Ready:              {Prefix: "🏄  "},
	Restarting:         {Prefix: "🔄  ", ShouldSpin: true},
	Running:            {Prefix: "🏃  ", ShouldSpin: true}, // this is used when minikube start for a second time (already started)
	Sparkle:            {Prefix: "✨  "},
	Stopped:            {Prefix: "🛑  "},
	Stopping:           {Prefix: "✋  "},
	Success:            {Prefix: "✅  "},
	ThumbsDown:         {Prefix: "👎  "},
	ThumbsUp:           {Prefix: "👍  "},
	Unpause:            {Prefix: "⏯️  "},
	URL:                {Prefix: "👉  ", LowPrefix: LowIndent},
	Usage:              {Prefix: "💡  "},
	Waiting:            {Prefix: "⌛  "},
	WaitingWithSpinner: {Prefix: "⌛  ", ShouldSpin: true},
	Unsupported:        {Prefix: "🚡  "},
	Workaround:         {Prefix: "👉  ", LowPrefix: LowIndent},

	// Fail emoji's
	Conflict:         {Prefix: "💢  ", LowPrefix: LowWarning},
	Failure:          {Prefix: "❌  ", LowPrefix: LowError},
	Fatal:            {Prefix: "💣  ", LowPrefix: LowError},
	Warning:          {Prefix: "❗  ", LowPrefix: LowWarning},
	KnownIssue:       {Prefix: "🧯  ", LowPrefix: LowError},
	UnmetRequirement: {Prefix: "⛔  ", LowPrefix: LowError},
	NotAllowed:       {Prefix: "🚫  ", LowPrefix: LowError},
	Embarrassed:      {Prefix: "🤦  ", LowPrefix: LowWarning},
	Sad:              {Prefix: "😿  "},
	Shrug:            {Prefix: "🤷  "},
	Improvement:      {Prefix: "💨  ", LowPrefix: LowWarning},
	SeeNoEvil:        {Prefix: "🙈  ", LowPrefix: LowError},

	// Specialized purpose styles
	AddonDisable:     {Prefix: "🌑  "},
	AddonEnable:      {Prefix: "🌟  "},
	Caching:          {Prefix: "🤹  "},
	Celebrate:        {Prefix: "🎉  "},
	Connectivity:     {Prefix: "📶  "},
	Containerd:       {Prefix: "📦  "},
	ContainerRuntime: {Prefix: "🎁  "},
	Copying:          {Prefix: "✨  "},
	CRIO:             {Prefix: "🎁  "}, // This should be a snow-flake, but the emoji has a strange width on macOS
	DeletingHost:     {Prefix: "🔥  "},
	Docker:           {Prefix: "🐳  ", ShouldSpin: true},
	DryRun:           {Prefix: "🌵  "},
	Enabling:         {Prefix: "🔌  "},
	FileDownload:     {Prefix: "💾  "},
	Fileserver:       {Prefix: "🚀  "},
	HealthCheck:      {Prefix: "🔎  "},
	Internet:         {Prefix: "🌐  "},
	ISODownload:      {Prefix: "💿  "},
	Kubectl:          {Prefix: "💗  "},
	Meh:              {Prefix: "🙄  ", LowPrefix: LowWarning},
	Mounting:         {Prefix: "📁  "},
	MountOptions:     {Prefix: "💾  "},
	Permissions:      {Prefix: "🔑  "},
	Provisioner:      {Prefix: "ℹ️  "},
	Pulling:          {Prefix: "🚜  "},
	Resetting:        {Prefix: "🔄  "},
	Shutdown:         {Prefix: "🛑  "},
	StartingNone:     {Prefix: "🤹  "},
	StartingSSH:      {Prefix: "🔗  "},
	StartingVM:       {Prefix: "🔥  ", ShouldSpin: true},
	SubStep:          {Prefix: "    ▪ ", LowPrefix: LowIndentBullet, ShouldSpin: true, HideAfterSpin: true},
	Tip:              {Prefix: "💡  "},
	Unmount:          {Prefix: "🔥  "},
	VerifyingNoLine:  {Prefix: "🤔  "},
	Verifying:        {Prefix: "🤔  "},
	CNI:              {Prefix: "🔗  "},
	Toolkit:          {Prefix: "🛠️   "},
}

// LowPrefix returns a 7-bit compatible prefix for a style
func LowPrefix(s Options) string {
	if s.LowPrefix != "" {
		return s.LowPrefix
	}
	if strings.HasPrefix(s.Prefix, "  ") {
		return LowIndent
	}
	return LowBullet
}
