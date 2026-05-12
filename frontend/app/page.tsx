import { createClient } from "@/lib/supabase/server";
import MapComponent from "@/components/homeComponents/Map";
import { DataTable } from "../components/homeComponents/table";
import { columns } from "../components/homeComponents/columns";
import LenHeader from "@/components/homeComponents/header";
import GymList from "@/components/homeComponents/gym-list";

interface Gym {
  id: string;
  name: string;
  network: string;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  hours: Record<string, string>;
  link: string;
}

const Home = async () => {
  const supabase = await createClient();

  const { data } = await supabase.from("gyms").select("*");
  const gymsData = (data as Gym[]) || [];

  return (
    <div className="h-auto w-full flex flex-col justify-center bg-primary--foreground items-center">
      <div className="xl:w-6/8 lg:w-8/9 md:w-8/9 sm:w-8/9 w-full h-full">
        <LenHeader dataLen={gymsData.length} />
        <MapComponent gyms={gymsData as unknown as []} />
        <GymList gyms={gymsData} />
        <div className="hidden sm:inline w-0 ">
          <DataTable data={gymsData} columns={columns} />
        </div>
      </div>
    </div>
  );
};

export default Home;
