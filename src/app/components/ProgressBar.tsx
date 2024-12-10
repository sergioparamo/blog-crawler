import React from 'react';

interface ProgressBarProps {
  progress: number;
  status: string;
}

export function ProgressBar({ progress, status }: ProgressBarProps) {
  return (
    <div className="space-y-4">
      <div className="relative w-full bg-gray-200 rounded-full h-8">
        <div
          className="bg-indigo-600 h-8 rounded-full transition-all duration-500 flex items-center justify-center text-white text-sm font-medium"
          style={{ width: `${progress}%` }}
        >
          {progress.toFixed(1)}%
        </div>
      </div>
      <p className="text-sm text-gray-600">{status}</p>
    </div>
  );
}