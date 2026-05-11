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

const Hours = ({ hours }: { hours: Record<string, string> }) => {
  const formatTime = (timeRange: string) => {
    return timeRange.replace(/:00/g, "");
  };

  return (
    <div className="w-full mt-3">
      <h1 className="font-bold text-lg " >Godziny otwarcia:</h1>
      <ul className="space-y-1 mt-2">
        {DAYS_ORDER.map(({ key, label }) => {
          const time = hours[key];
          return (
            <li key={key} className="flex justify-between text-sm">
              <span>{label}</span>
              <span>{time ? formatTime(time) : "Zamknięte"}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default Hours;
