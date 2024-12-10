import React, { useState, useRef, useEffect } from "react";

interface LogBoxProps {
  logs: string[];
}

export function LogBox({ logs }: LogBoxProps) {
  const [width, setWidth] = useState("auto");
  const [height, setHeight] = useState('30vh');
  const [x] = useState(0);
  const [y] = useState(0);
  const logBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const logBox = logBoxRef.current;
    if (logBox) {
      const parentWidth = logBox.parentElement?.clientWidth || 0;
      const parentHeight = logBox.parentElement?.clientHeight || 0;
      setWidth(`${parentWidth}px`);
      setHeight(`${parentHeight}px`);
    }
  }, []);

  // Scroll to the bottom of the log box whenever logs change
  useEffect(() => {
    const logBox = logBoxRef.current;
    if (logBox) {
      logBox.scrollTop = logBox.scrollHeight; // Scrolls to the bottom
    }
  }, [logs]);

  const handleMouseDown = (event: React.MouseEvent<HTMLDivElement>) => {
    const logBox = logBoxRef.current;
    if (!logBox) return;

    const startX = event.clientX;
    const startY = event.clientY;
    const initialWidth = width;
    const initialHeight = height;

    const handleMouseMove = (event: MouseEvent) => {
      const newWidth = initialWidth + (event.clientX - startX);
      const newHeight = initialHeight + (event.clientY - startY);
      setWidth(`${newWidth}px`);
      setHeight(`${newHeight}px`);
    };

    const handleMouseUp = () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
  };

  return (
    <div>
      <style>
        {`
          .log-box {
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #333;
            resize: both;
            overflow: auto;
            margin-top: 20px;
          }
        `}
      </style>
      <div
        ref={logBoxRef}
        className="log-box"
        style={{
          width,
          height,
          left: x,
          top: y,
        }}
        onMouseDown={handleMouseDown}
      >
        {logs.map((log, index) => (
          <div key={index} className="text-gray-300">
            {log}
          </div>
        ))}
      </div>
    </div>
  );
}
