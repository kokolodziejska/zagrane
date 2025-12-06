import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

export interface ReservationDraft {
  objectId: number;
  date: string;
  start: string;
  duration: number;
  split: boolean;
  players: number;
  acceptedRules: boolean;
  total: number;
  userTotal: number;
}

const initialState: ReservationDraft = {
  objectId: 0,
  date: '',
  start: '',
  duration: 60,
  split: false,
  players: 1,
  acceptedRules: false,
  total: 0,
  userTotal: 0,
};

const reservationSlice = createSlice({
  name: 'reservation',
  initialState,
  reducers: {
    setReservationDraft: (_state, action: PayloadAction<ReservationDraft>) => {
      return action.payload;
    },
  },
});

export const { setReservationDraft } = reservationSlice.actions;
export default reservationSlice.reducer;
