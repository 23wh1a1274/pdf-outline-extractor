import React from "react";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

function PDFViewer({ pdfData, jumpToPage }) {
  return (
    <div>
      {pdfData ? (
        <Document file={{ data: pdfData }}>
          <Page pageNumber={jumpToPage} />
        </Document>
      ) : (
        <p>No PDF file loaded</p>
      )}
    </div>
  );
}

export default PDFViewer;
