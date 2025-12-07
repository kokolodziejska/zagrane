'use client';

import * as React from 'react';
import { CalendarIcon } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';

import { useEffect, useState } from 'react';

import { useAppDispatch } from '@/store/hooks';
import { useAppSelector } from '@/store/hooks';
import { setPickedDate } from '@/store/userState';
import { selectIsLogin, selectPickedDate } from '@/store/selectors';

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

function DatePicker() {
  const picked = useAppSelector(selectPickedDate);
  const dispatch = useAppDispatch();

  const [open, setOpen] = React.useState(false);
  const [date, setDate] = React.useState<Date | undefined>(new Date('2025-06-01'));
  const [month, setMonth] = React.useState<Date | undefined>(date);
  const [value, setValue] = React.useState(formatDate(date));

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  useEffect(() => {
    const d = fromISO(picked);
    setMonth(d);
    setValue(formatDate(d));
    setDate(d);
  }, [picked]);

  return (
    <div className="flex flex-col gap-3">
      <Label htmlFor="date" className="px-1">
        Wybierz dzień
      </Label>
      <div className="relative flex gap-2">
        <Input
          id="date"
          value={value}
          className="bg-background pr-10"
          onChange={(e) => {
            const date = new Date(e.target.value);
            setValue(e.target.value);
            if (isValidDate(date)) {
              dispatch(setPickedDate(toISO(date)));
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
              disabled={(d) => d < today}
              onMonthChange={setMonth}
              onSelect={(date) => {
                if (date) {
                  dispatch(setPickedDate(toISO(date)));
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
