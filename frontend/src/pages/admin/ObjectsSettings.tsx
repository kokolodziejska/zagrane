import ObjectsSettingsTable from '@/components/admin/objectsettings/ObjectsSettingsTable';
import { useEffect, useState } from 'react';
import ObjectForm from '@/components/admin/objectsettings/ObjectForm';

type Object = {
  id: number;
  name: string;
  discipline: string;
  description: string;
  opening_hour: string;
  closing_hour: string;
  time_block: number;
  minimal_time_block: number;
  maximal_time_block: number;
};

async function get_objects() {
  try {
    const res = await fetch(`/api/objects/`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error('Error fetching objects:', err);
    return [];
  }
}
async function get_nextId() {
  try {
    const res = await fetch(`/api/objects/next_free_id`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error('Error fetching objects:', err);
    return [];
  }
}

function ObjectsSettings() {
  const [objects, setObjects] = useState<Object[]>([]);
  const [nextId, setNextId] = useState<number>(0);

  async function refreshGlobal() {
    const objs = await get_objects();
    setObjects(objs);
    refres_NextId();
  }
  async function refres_NextId() {
    const id = await get_nextId();
    setNextId(id.id);
  }

  useEffect(() => {
    refreshGlobal();
    refres_NextId();
  }, []);

  if (!objects || !nextId) return <p>Loading...</p>;

  return (
    <div>
      <div className="container flex flex-col items-center justify-center w-[80vw] margin-[5vh] gap-[2vw] pb-[10vh]">
        <h2 className="text-4xl font-bold"> Ustawienia obiektów</h2>
        <ObjectsSettingsTable objectsSettings={objects} onSaved={refreshGlobal} />
        <ObjectForm objectId={nextId} onSaved={refreshGlobal}></ObjectForm>
      </div>
    </div>
  );
}

export default ObjectsSettings;
