// src/components/Notes.js
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const Notes = () => {
  const [notes, setNotes] = useState([]);
  const [noteIndex, setNoteIndex] = useState(0);

  // Sample notes to simulate incoming notes
  const sampleNotes = [
    "1. Meeting started, discussing project goals.",
    "2. Key objectives: Improve user experience and increase engagement.",
    "3. Action item: Schedule a follow-up meeting for next week.",
    "4. Assign tasks to team members based on expertise.",
    "5. Discuss budget constraints and resource allocation.",
    "6. Note: Focus on mobile responsiveness for the next release.",
    "7. Set deadlines for initial deliverables.",
    "8. Meeting adjourned, awaiting further updates."
  ];

  useEffect(() => {
    // Function to add the next note to the displayed list
    const addNote = () => {
      setNotes((prevNotes) => [
        ...prevNotes,
        sampleNotes[noteIndex],
      ]);
      setNoteIndex((prevIndex) => prevIndex + 1);
    };

    // Initialize interval only if there are more notes to add
    const intervalId = setInterval(() => {
      if (noteIndex < sampleNotes.length) {
        addNote();
      }
    }, 10000); // Update every 10 seconds

    return () => clearInterval(intervalId); // Clean up interval on component unmount
  }, [noteIndex, sampleNotes]);

  return (
    <div style={{ padding: '20px', height: '100%', overflowY: 'scroll' }}>
      <ReactMarkdown>{notes.join("\n\n")}</ReactMarkdown>
    </div>
  );
};

export default Notes;
