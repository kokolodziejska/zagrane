import { useEffect, useState } from 'react';
import TimeSettings from '@/components/admin/globalsettings/time/TimeSettings';
import TimeSettingsForm from '@/components/admin/globalsettings/time/TimeSettingsForm';
import Disciplineettings from '@/components/admin/globalsettings/discipline/DisciplineSettings';
import NumberOfPlayersSettings from '@/components/admin/globalsettings/players/NumberOfPlayersSettings';

type GlobalSettings = {
  openingHour: string;
  closingHour: string;

  timeBlock: number;
  minimalTimeBlock: number;
  maximalTimeBlock: number;
  minBookingAdvanceTime: number;
  minCacncelTime: number;
  currency: string;

  defaultPlayers: number;
  defaultDiscipline: string;
  availableDisciplines: string[];
};

async function get_global() {
  try {
    const res = await fetch(`/api/global_settings/get_full_global_company_settings`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error('Error fetching global settings:', err);
    return null;
  }
}

function GlobalSettings() {
  const [globalSettings, setGlobalSettings] = useState<GlobalSettings | null>(null);

  async function refreshGlobal() {
    const data = await get_global();
    setGlobalSettings(data);
  }

  useEffect(() => {
    refreshGlobal();
  }, []);

  if (!globalSettings) return <p>Loading...</p>;

  return (
    <div>
      <div className="container flex flex-col items-center w-[80vw] margin-[2vh] gap-[1vw] pb-[10vh]">
        <div className="container flex flex-col items-center w-[80vw] gap-[2vw] margin-[2vh]">
          <h1 className="text-4xl font-bold pt-[2vh]">Ustawienia globalne firmy</h1>
          <TimeSettings globalSettings={globalSettings}></TimeSettings>
          <TimeSettingsForm globalSettings={globalSettings} onSaved={refreshGlobal} />
        </div>
        <div className="admin-horisontal-line"></div>
        <div className="flex flex-row gap-[3vw]">
          <div className="pt-[2vh]">
            <Disciplineettings globalSettings={globalSettings} />
          </div>
          <div className="admin-vertical-line"></div>
          <div className="pt-[2vh]">
            <NumberOfPlayersSettings defPlayers={globalSettings.defaultPlayers} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default GlobalSettings;
