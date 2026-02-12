const moods = [
  { value: 1, emoji: "😞", label: "Very low" },
  { value: 3, emoji: "😕", label: "Low" },
  { value: 5, emoji: "😐", label: "Okay" },
  { value: 7, emoji: "🙂", label: "Good" },
  { value: 9, emoji: "😊", label: "Great" }
]

export default function MoodScale({ value, onSelect }: any) {
  return (
    <>
      <h2>How are you feeling today?</h2>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        {moods.map(m => (
          <button
            key={m.value}
            onClick={() => onSelect(m.value)}
            style={{
              fontSize: 28,
              background: value === m.value ? "#bbdefb" : "transparent",
              borderRadius: 12,
              border: "none",
              padding: 8
            }}
          >
            {m.emoji}
          </button>
        ))}
      </div>
    </>
  )
}
