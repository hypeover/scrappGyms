"use client"
import React, { useEffect } from "react";
import {
  Map,
  MapLayerGroup,
  MapLayers,
  MapLayersControl,
  MapMarker,
  MapPopup,
  MapTileLayer,
  MapControlContainer,
  MapMarkerClusterGroup,
  MapTooltip,
} from "@/components/ui/map";
import { MapPin } from "lucide-react";
import {
  Card,
  CardTitle,
  CardContent,
  CardFooter
} from "@/components/ui/card";
import Hours from '@/components/homeComponents/hours'

const networkColors = {
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

const MapComponent = ({
  gyms,
}: {
  gyms: {
    id: string;
    network: string;
    latitude: number;
    longitude: number;
    city: string;
    address: string;
    hours: Record<string, string>;
    link: string;
  }[];
}) => {
  const unique_networks = [...new Set(gyms.map((item) => item.network))];
  const [mounted, setMounted] = React.useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);


  return (
    <div className={`rounded-xl h-200 shadow-xl w-6/8 transition-opacity duration-1000 ${mounted ? 'opacity-100' : 'opacity-0'}`}>
      <Map className="rounded-xl h-full shadow-xl" center={[51.919438, 19.145136]} zoom={7}>
        <MapLayers
          defaultLayerGroups={unique_networks.map((network) => network)}
        >
          <MapLayersControl />
          <MapTileLayer />
          <MapTileLayer
            name="No Labels"
            url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
            darkUrl="https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png"
          />
          {unique_networks.map((network) => (
            <MapLayerGroup name={network} key={network}>
              <MapMarkerClusterGroup>
                {gyms
                  .filter((gym) => gym.network === network)
                  .map((gym) => {
                    const markerColor = networkColors[gym.network] || "black";

                    return (
                      <MapMarker
                        key={gym.id}
                        position={[gym.latitude, gym.longitude]}
                        icon={<MapPin color={markerColor} />}
                      >
                        <MapTooltip side="top">{gym.network}</MapTooltip>
                        <MapPopup className="rounded-xl py-1 px-0" >
                          <Card className="gap-0 px-4 py-2.5 b-none outline-0 ring-0 shadow-none">
                            <CardTitle className="text-xl font-bold text-left" ><a target="_blank" href={gym.link}>{gym.network}</a></CardTitle>
                            <CardContent className="text-left p-0 mt-3">
                              <p className="text-lg font-bold" >{gym.city}</p>
                              <br/>
                              <p>{gym.address}</p>
                              <CardFooter className="w-full p-0" >
                                <Hours hours={gym.hours} />
                              </CardFooter>
                            </CardContent>
                          </Card>
                        </MapPopup>
                      </MapMarker>
                    );
                  })}
              </MapMarkerClusterGroup>
            </MapLayerGroup>
          ))}
          <MapControlContainer className="bg-popover text-popover-foreground bottom-1 left-1 flex flex-col gap-2 rounded-md border p-2 shadow">
            {Object.entries(networkColors).map(([networkName, color]) => (
              <div key={networkName} className="flex items-center gap-3 rounded-xl">
                <div
                  className="w-3 h-3 rounded-full border border-gray-200"
                  style={{ backgroundColor: color }}
                />
                <span className="text-sm font-medium text-gray-700">
                  {networkName}
                </span>
              </div>
            ))}
          </MapControlContainer>
        </MapLayers>
      </Map>
    </div>
  );
};

export default MapComponent;
