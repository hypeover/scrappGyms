import { createClient } from '@/lib/supabase/server';
import MapComponent from '@/components/homeComponents/Map';
import { DataTable } from '../components/homeComponents/table';
import { columns } from '../components/homeComponents/columns';
import LenHeader from '@/components/homeComponents/header';

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
  
  const { data } = await supabase.from('gyms').select('*');
  const gymsData = (data as Gym[]) || [];

  return (
    <div className='h-auto w-full flex flex-col justify-center bg-primary--foreground items-center'>
      <LenHeader dataLen={gymsData.length} />
      <MapComponent gyms={gymsData as unknown as []} />
      <DataTable data={gymsData} columns={columns} />
    </div>
  )
}

export default Home

