import PriceSettingsTableMaster from '@/components/admin/pricesettings/PriceSettingsTableMaser';
import { useEffect, useState } from 'react';

type Price = {
  id: number;
  price_table: number;
  object_id: number;
  valid_from: Date;
  valid_to: Date;
  name: string;
  day_mask: number;
  start_hour: string;
  end_hour: string;
  duration: number;
  price: number;
  price_with_pass: number;
};

async function get_prices() {
  try {
    const res = await fetch(`/api/prices/`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error('Error fetching objects:', err);
    return [];
  }
}

function PriceSettings() {
  const [prices, setPrices] = useState<Price[]>([]);

  async function refresSettings() {
    const objs = await get_prices();
    setPrices(objs);
  }

  useEffect(() => {
    refresSettings();
  }, []);

  return (
    <div>
      <div className="container flex flex-col items-center w-[80vw] margin-[2vh] gap-[1vw] pb-[10vh]">
        <PriceSettingsTableMaster priceSettings={prices} />
      </div>
    </div>
  );
}

export default PriceSettings;
