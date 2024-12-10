import React from 'react';
import { ChevronDownIcon } from './Icons';

interface YearSelectorProps {
  startYear: number;
  endYear: number;
  populateBetween: boolean;
  proxies: boolean;
  onStartYearChange: (year: number) => void;
  onEndYearChange: (year: number) => void;
  onPopulateBetweenChange: (value: boolean) => void;
  onProxiesChange: (value: boolean) => void;
}

export function YearSelector({
  startYear,
  endYear,
  populateBetween,
  proxies,
  onStartYearChange,
  onEndYearChange,
  onPopulateBetweenChange,
  onProxiesChange,
}: YearSelectorProps) {
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 1990 + 1 }, (_, i) => currentYear - i);

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="relative">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Start Year
          </label>
          <select
            value={startYear}
            onChange={(e) => onStartYearChange(Number(e.target.value))}
            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md appearance-none"
          >
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
          <ChevronDownIcon className="absolute right-3 top-9 h-4 w-4 text-gray-400" />
        </div>
        <div className="relative">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            End Year
          </label>
          <select
            value={endYear}
            onChange={(e) => onEndYearChange(Number(e.target.value))}
            className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md appearance-none"
          >
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
          <ChevronDownIcon className="absolute right-3 top-9 h-4 w-4 text-gray-400" />
        </div>
      </div>
      <div className="flex items-center">
        <input
          type="checkbox"
          id="populate-between"
          checked={populateBetween}
          onChange={(e) => onPopulateBetweenChange(e.target.checked)}
          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
        />
        <label htmlFor="populate-between" className="ml-2 block text-sm text-gray-700">
          Include years in between
        </label>
      </div>
      <div className="flex items-center">
        <input
          type="checkbox"
          id="proxies"
          checked={proxies}
          onChange={(e) => onProxiesChange(e.target.checked)}
          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          disabled={true}
        />
        <label htmlFor="proxies" className="ml-2 block text-sm text-gray-700">
          Add proxy (Coming soon...)
        </label>
      </div>
    </div>
  );
}