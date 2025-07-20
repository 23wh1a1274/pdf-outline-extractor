import React, { useState } from "react";

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [outlineData, setOutlineData] = useState(null);
  const [expandedH1, setExpandedH1] = useState({});

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) setPdfFile(file);
  };

  const extractOutline = async () => {
    if (!pdfFile) return;

    const formData = new FormData();
    formData.append("pdf", pdfFile);

    try {
      const res = await fetch("http://localhost:5000/extract-outline", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setOutlineData(data);
    } catch (err) {
      console.error("Failed to fetch outline", err);
    }
  };

  const toggleH1 = (index) => {
    setExpandedH1((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const groupOutline = (outline) => {
    const grouped = [];
    let currentH1 = null;

    outline.forEach((item) => {
      if (item.level === "H1") {
        currentH1 = { ...item, children: [] };
        grouped.push(currentH1);
      } else if (item.level === "H2" && currentH1) {
        currentH1.children.push(item);
      }
    });

    return grouped;
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Segoe UI, sans-serif" }}>
      <h1>📄 PDF Outline Extractor</h1>

      <div style={{ marginBottom: "1rem" }}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button
          onClick={extractOutline}
          style={{
            marginLeft: "1rem",
            padding: "0.5rem 1rem",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Extract Outline
        </button>
      </div>

      {outlineData && (
        <div>
          <h2 style={{ color: "#333" }}>📘 Title: {outlineData.title}</h2>
          <div>
            {groupOutline(outlineData.outline).map((h1, idx) => (
              <div key={idx} style={{ marginTop: "1rem" }}>
                <div
                  onClick={() => toggleH1(idx)}
                  style={{
                    cursor: "pointer",
                    fontWeight: "bold",
                    fontSize: "1.1rem",
                    background: "#f0f0f0",
                    padding: "0.5rem",
                    borderRadius: "5px",
                  }}
                >
                  ▶ {h1.text} (Page {h1.page})
                </div>
                {expandedH1[idx] && h1.children.length > 0 && (
                  <ul style={{ marginLeft: "1.5rem", marginTop: "0.5rem" }}>
                    {h1.children.map((h2, i) => (
                      <li key={i}>
                        {h2.text} <span style={{ color: "#555" }}>(Page {h2.page})</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
