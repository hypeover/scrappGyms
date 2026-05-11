import { createClient } from '@/lib/supabase/server';
import MapComponent from './Map';
import Charts from './charts';

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
      <h1 className='font-semibold my-5 text-3xl font-mono' >Aktualnie na mapie jest {gymsData.length} obiektów.</h1>
      <MapComponent gyms={gymsData as unknown as []} />
      <Charts />
    </div>
  )
}

export default Home

