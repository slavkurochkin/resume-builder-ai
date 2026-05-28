function formatResume() {
  const doc = DocumentApp.getActiveDocument();
  const body = doc.getBody();
  const paragraphs = body.getParagraphs();

  // Format the very first non-empty paragraph (Name)
  const firstP = paragraphs.find(p => p.getText().trim().length > 0);
  if (firstP) {
    firstP.setHeading(DocumentApp.ParagraphHeading.HEADING2);
    firstP.setBold(true);
  }

  paragraphs.forEach(p => {
    const text = p.getText().trim();  // trim before every check

    // Format section headers
    if (/^(Professional Summary|Work Experience|Skills|Certifications|Education|Projects)$/i.test(text)) {
      p.setHeading(DocumentApp.ParagraphHeading.HEADING4);
      p.setBold(true);
      p.setForegroundColor('#000000');
    }

    // Format company names
    if (/^(Self-Directed|Zillow|LTK|Automox|Jiveworld|Paylocity|Epic Loan Systems)$/i.test(text)) {
      p.setBold(true);
      p.setForegroundColor('#1F4FD8');
    }
  });
}
