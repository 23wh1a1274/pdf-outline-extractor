import React, { useState } from 'react';
import axios from 'axios';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [outline, setOutline] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF");

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await axios.post("http://localhost:5000/extract-outline", formData);
      setOutline(response.data);
    } catch (err) {
      console.error("Error uploading:", err);
      alert("Upload failed. Check console.");
    }
  };

  return (
    <div className="upload-form">
      <h2>PDF Outline Extractor</h2>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload & Extract</button>

      {outline && (
        <div className="outline">
          <h3>Title: {outline.title}</h3>
          <ul>
            {outline.outline.map((item, index) => (
              <li key={index}>
                {item.level}: {item.text} (Page {item.page})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default UploadForm;
