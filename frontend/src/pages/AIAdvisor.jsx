import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getAIAdvice } from "../services/api";

export default function AIAdvisor() {
  const { id } = useParams();
  const [text, setText] = useState("Analyzing...");

  useEffect(() => {
    getAIAdvice(id)
      .then(r => setText(r.data.response))
      .catch(() => setText("Unable to generate analysis."));
  }, [id]);

  return (
    <div>
      <h1>AI Academic Advisor</h1>
      <div className="ai-response">
        <pre>{text}</pre>
      </div>
    </div>
  );
}
