import { createClient } from '@/lib/supabase/server';
import MapComponent from './Map';

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
    <div className='h-screen w-full'>
      <MapComponent gyms={gymsData as unknown as []} />
    </div>
  )
}

export default Home
