'use client';

import * as React from 'react';
import { CalendarIcon } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';

import { useEffect, useState } from 'react';

const toISO = (d: Date): string => {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
};

const fromISO = (s: string): Date => {
  const [y, m, d] = s.split('-').map(Number);
  return new Date(y, m - 1, d);
};

function formatDate(date: Date | undefined) {
  if (!date) {
    return '';
  }

  return date.toLocaleDateString('pl-PL', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
}

function isValidDate(date: Date | undefined) {
  if (!date) {
    return false;
  }
  return !isNaN(date.getTime());
}

type DatePickerProps = {
  /** Data w formacie 'YYYY-MM-DD' */
  value?: string;
  /** Zwracana na zewnątrz data (ISO) przy każdej zmianie */
  onChange?: (value: string) => void;
};

function DatePicker({ value: valueProp, onChange }: DatePickerProps) {
  const [open, setOpen] = useState(false);

  // Ustal początkową datę: z propsów albo domyślną
  const initialDate = valueProp ? fromISO(valueProp) : new Date('2025-06-01');

  const [date, setDate] = useState<Date | undefined>(initialDate);
  const [month, setMonth] = useState<Date | undefined>(initialDate);
  const [inputValue, setInputValue] = useState(formatDate(initialDate));

  const today = new Date();
  today.setHours(0, 0, 0, 0);


  useEffect(() => {
    if (!valueProp) return;

    const d = fromISO(valueProp);
    setDate(d);
    setMonth(d);
    setInputValue(formatDate(d));
  }, [valueProp]);

  const handleDateChange = (newDate: Date) => {
    setDate(newDate);
    setMonth(newDate);
    setInputValue(formatDate(newDate));

    const iso = toISO(newDate);
    onChange?.(iso); 
  };

  return (
    <div className="flex flex-col gap-3">
      <Label htmlFor="date" className="px-1">
        Wybierz dzień
      </Label>
      <div className="relative flex gap-2">
        <Input
          id="date"
          value={inputValue}
          className="bg-background pr-10"
          onChange={(e) => {
            const text = e.target.value;
            setInputValue(text);

            const parsed = new Date(text);
            if (isValidDate(parsed)) {
              handleDateChange(parsed);
            }
          }}
          onKeyDown={(e) => {
            if (e.key === 'ArrowDown') {
              e.preventDefault();
              setOpen(true);
            }
          }}
        />
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              id="date-picker"
              variant="ghost"
              className="absolute top-1/2 right-2 size-6 -translate-y-1/2"
            >
              <CalendarIcon className="size-3.5" />
              <span className="sr-only">Select date</span>
            </Button>
          </PopoverTrigger>
          <PopoverContent
            className="w-auto overflow-hidden p-0"
            align="end"
            alignOffset={-8}
            sideOffset={10}
          >
            <Calendar
              mode="single"
              selected={date}
              captionLayout="dropdown"
              month={month}
              onMonthChange={setMonth}
              onSelect={(selectedDate) => {
                if (selectedDate) {
                  handleDateChange(selectedDate);
                  setOpen(false);
                }
              }}
            />
          </PopoverContent>
        </Popover>
      </div>
    </div>
  );
}

export default DatePicker;
