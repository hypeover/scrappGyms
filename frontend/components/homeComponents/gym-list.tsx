import React from "react";
import { InfiniteSlider } from "@/components/motion-primitives/infinite-slider";

const networkColors: Record<string, string> = {
  JustGym: "#f9b617",
  Zdrofit: "#0099de",
  "Fitness Academy": "#ee3030",
  "Fabryka Formy": "#ee3030",
  Calypso: "#9dc75d",
  CityFit: "#3560f2",
  FitFabric: "#42d161",
  "Xtreme Fitness": "#2e337b",
  WellFitness: "#b4cb20",
};

const GymList = ({
  gyms,
}: {
  gyms: {
    network: string;
  }[];
}) => {

  return (
    <div className="py-10 w-full">
      <InfiniteSlider>
        {Object.entries(networkColors).map(([networkName, color], key) => (
          <div
            style={{ backgroundColor: color }}
            className="p-2 text-white font-mono rounded-xl font-semibold"
            key={key}
          >
            {networkName}:{" "}
            {gyms.filter((item) => item.network === networkName).length}
          </div>
        ))}
      </InfiniteSlider>
    </div>
  );
};

export default GymList;
