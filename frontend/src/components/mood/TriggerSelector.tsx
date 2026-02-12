const triggersList = [
  "Stress",
  "Loneliness",
  "Boredom",
  "Social pressure",
  "Anxiety",
  "Anger"
]

export default function TriggerSelector({ selected, onChange }: any) {
  const toggle = (t: string) => {
    onChange(
      selected.includes(t)
        ? selected.filter((x: string) => x !== t)
        : [...selected, t]
    )
  }

  return (
    <>
      <h2>Any triggers today?</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        {triggersList.map(t => (
          <button
            key={t}
            onClick={() => toggle(t)}
            style={{
              padding: "6px 12px",
              borderRadius: 20,
              border: selected.includes(t)
                ? "2px solid #1976d2"
                : "1px solid #ccc",
              background: selected.includes(t) ? "#e3f2fd" : "#fff"
            }}
          >
            {t}
          </button>
        ))}
      </div>
    </>
  )
}
