export default function SuccessScreen() {
  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2>🌱 Check-in complete</h2>
        <p>You showed up today. That matters.</p>
        <p>One step at a time. Keep going 💙</p>

        <a href="/dashboard" style={styles.link}>
          Back to Dashboard
        </a>
      </div>
    </div>
  )
}

const styles: any = {
  page: {
    minHeight: "100vh",
    background: "#e3f2fd",
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  },
  card: {
    background: "#fff",
    padding: 24,
    borderRadius: 16,
    textAlign: "center",
    maxWidth: 360
  },
  link: {
    display: "block",
    marginTop: 16,
    color: "#1976d2"
  }
}
