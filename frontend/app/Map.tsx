import React from "react";
import {
  Map,
  MapLayerGroup,
  MapLayers,
  MapLayersControl,
  MapMarker,
  MapPopup,
  MapTileLayer,
  MapZoomControl,
} from "@/components/ui/map";
const MapComponent = ({
  gyms,
}: {
  gyms: {
    id: string;
    network: string;
    latitude: number;
    longitude: number;
  }[];
}) => {
  const unique_networks = [...new Set(gyms.map((item) => item.network))];

  console.log(unique_networks);

  return (
    <Map className="h-full" center={[51.919438, 19.145136]} zoom={7}>
      <MapLayers defaultLayerGroups={unique_networks.map((network) => network)}>
        <MapLayersControl />
        <MapTileLayer />
        <MapTileLayer
          name="No Labels"
          url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
          darkUrl="https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png"
        />
        {unique_networks.map((network) => (
          <MapLayerGroup name={network} key={network}>
            {gyms
              .filter((gym) => gym.network === network)
              .map((gym) => (
                <MapMarker
                  key={gym.id}
                  position={[gym.latitude, gym.longitude]}
                ></MapMarker>
              ))}
          </MapLayerGroup>
        ))}
      </MapLayers>
    </Map>
  );
};

export default MapComponent;