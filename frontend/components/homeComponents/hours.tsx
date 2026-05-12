import React from "react";

const DAYS_ORDER = [
  { key: "Monday", label: "Poniedziałek" },
  { key: "Tuesday", label: "Wtorek" },
  { key: "Wednesday", label: "Środa" },
  { key: "Thursday", label: "Czwartek" },
  { key: "Friday", label: "Piątek" },
  { key: "Saturday", label: "Sobota" },
  { key: "Sunday", label: "Niedziela" },
] as const;

const formatOpeningHours = (rawTime: string | undefined) => {
  if (!rawTime) return "Zamknięte";
  
  return rawTime
    .split('-')
    .map(time => {
      const parts = time.trim().split(':');
      const hours = parts[0].padStart(2, '0');
      const minutes = parts[1] ? parts[1].padStart(2, '0') : '00';
      
      return `${hours}:${minutes}`;
    })
    .join(' - '); 
};

const Hours = ({ hours }: { hours: Record<string, string> }) => {
  return (
    <div className="w-full mt-3">
      <h1 className="font-bold text-lg">Godziny otwarcia:</h1>
      <ul className="space-y-1 mt-2">
        {DAYS_ORDER.map(({ key, label }) => {
          const time = hours[key];
          return (
            <li key={key} className="flex justify-between text-base font-normal">
              <span className="text-zinc-600">{label}</span>
              <span className="font-medium tabular-nums">
                {formatOpeningHours(time)}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default Hours;
