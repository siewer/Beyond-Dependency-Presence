package react

var (
	// Love reaction emoji.
	Love Emoji = "❤️"
	// Like reaction emoji.
	Like Emoji = "👍"
	// CatLove reaction emoji.
	CatLove Emoji = "😻"
	// LoveIt reaction emoji.
	LoveIt Emoji = "😍"
	// InLove reaction emoji.
	InLove Emoji = "🥰"
	// Heart reaction emoji (alias of Love).
	Heart = Love
	// Cheers reaction emoji.
	Cheers Emoji = "🥂"
	// Hot reaction emoji.
	Hot Emoji = "🔥"
	// Party reaction emoji.
	Party Emoji = "🎉"
	// Birthday reaction emoji.
	Birthday Emoji = "🎂️"
	// Sparkles reaction emoji.
	Sparkles Emoji = "✨"
	// Rainbow reaction emoji.
	Rainbow Emoji = "🌈"
	// Pride reaction emoji.
	Pride Emoji = "🏳️‍🌈"
	// SeeNoEvil reaction emoji.
	SeeNoEvil Emoji = "🙈"
	// Unknown reaction fallback.
	Unknown Emoji
)

// Reactions specifies reaction emojis by name.
var Reactions = map[string]Emoji{
	"love":        Love,
	"+1":          Like,
	"cat-love":    CatLove,
	"love-it":     LoveIt,
	"in-love":     InLove,
	"heart":       Heart,
	"cheers":      Cheers,
	"hot":         Hot,
	"party":       Party,
	"birthday":    Birthday,
	"sparkles":    Sparkles,
	"rainbow":     Rainbow,
	"pride":       Pride,
	"see-no-evil": SeeNoEvil,
}

// Names specifies the reaction names by emoji.
var Names = map[Emoji]string{
	Love:      "love",
	Like:      "+1",
	CatLove:   "cat-love",
	LoveIt:    "love-it",
	InLove:    "in-love",
	Heart:     "heart",
	Cheers:    "cheers",
	Hot:       "hot",
	Party:     "party",
	Birthday:  "birthday",
	Sparkles:  "sparkles",
	Rainbow:   "rainbow",
	Pride:     "pride",
	SeeNoEvil: "see-no-evil",
}
