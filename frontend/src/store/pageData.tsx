import { createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';


type ReadSection = {
  slug: string;
  title: string;
  path: string;
  elements: {
    element: string;
    prop: string;
  }[];
};

type ReadPage = {
  slug: string;
  title: string;
  basePath: string;
  type: string;
  mode: string;
  sections: ReadSection[];
};

export interface Pages {
  pages: ReadPage[];
  loading: boolean;
  error: boolean;
}

const initialState: Pages = { pages: [], loading: true, error: false };


export const fetchPages = createAsyncThunk<ReadPage[]>(
  'pages/fetch',
  async () => {
    const res = await fetch('/config/pages.json', { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data.pages as ReadPage[];
  }
);

const pagesSlice = createSlice({
  name: 'pages',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPages.pending, (state) => {
        state.loading = true;
        state.error = false;
      })
      .addCase(fetchPages.fulfilled, (state, action) => {
        state.loading = false;
        state.error = false;
        state.pages = action.payload;
      })
      .addCase(fetchPages.rejected, (state) => {
        state.loading = false;
        state.error = true;
      });
  },
});

export default pagesSlice.reducer;
