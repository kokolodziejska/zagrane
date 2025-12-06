import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

const today = new Date().toISOString().slice(0, 10);

export interface UserState {
  isLogin: boolean;
  userId: number;
  userEmail: string;
  userName: string;
  userSurname: string; 
  departmentId: number;
  departmentName: string;
  userRole: string;


  pickedDate: string;
  pickedObjectId: number | null;
  pickedStartHour: string | null;
}

const initialState: UserState = {
  userId: 0,
  isLogin: false,
  userEmail: '',
  userName: '',
  userSurname: '',
  departmentId: 0,
  departmentName: '',
  userRole: '',


  pickedDate: today,
  pickedObjectId: null,
  pickedStartHour: null,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUserProfile: (
      state,
      action: PayloadAction<
        Omit<UserState, 'isLogin' | 'pickedDate' | 'pickedObjectId' | 'pickedStartHour'>
      >
    ) => {
      state.isLogin = true;
      state.userId = action.payload.userId;
      state.userEmail = action.payload.userEmail;
      state.userName = action.payload.userName;
      state.userSurname = action.payload.userSurname;
      state.departmentId = action.payload.departmentId;
      state.departmentName = action.payload.departmentName;
      state.userRole = action.payload.userRole;
    },
    logout: () => initialState,

    setPickedDate: (state, action: PayloadAction<string>) => {
      state.pickedDate = action.payload;
    },
    setSelectedObject: (
      state,
      action: PayloadAction<{ pickedObjectId: number; pickedStartHour: string }>
    ) => {
      state.pickedObjectId = action.payload.pickedObjectId;
      state.pickedStartHour = action.payload.pickedStartHour;
    },
  },
});

export const { setUserProfile, logout, setPickedDate, setSelectedObject } = userSlice.actions;
export default userSlice.reducer;
