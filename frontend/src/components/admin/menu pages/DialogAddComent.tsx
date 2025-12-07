import { useState } from 'react';

import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

import DatePicker from './DatePicker';

type DialogAddCommentProps = {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  headers: string[];
  rows: (string | number)[][];
};

function DialogAddComment({ open, onOpenChange, headers, rows }: DialogAddCommentProps) {
  const [pickedDate, setPickedDate] = useState<string>('2025-06-01');
  const [comment, setComment] = useState<string>('');

  const handleGeneratePdf = () => {
    console.log('Generuj PDF dla daty:', pickedDate);
    console.log('Wiersze do PDF:', rows);
    console.log('Komentarz:', comment);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        className="
          w-[90vw]
          sm:w-[70vw]
          sm:max-w-[70vw]
          h-[70vh]
          justify-center items-center
        "
      >
        <DialogHeader>
          <DialogTitle>Wygeneruj plik PDF z uwagami</DialogTitle>
          <DialogDescription>
            Wybierz dzień, sprawdź wybrane pozycje i dopisz komentarz.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <DatePicker value={pickedDate} onChange={setPickedDate} />

          {/* Tabela z wybranymi wierszami */}
          <div className="border rounded-md max-h-[50vh] overflow-auto max-w-[65vw]">
            <Table className="min-w-max w-full">
              <TableHeader className="bg-gray-100 sticky top-0 z-10">
                <TableRow>
                  {headers.map((header, idx) => (
                    <TableHead
                      key={idx}
                      className="px-2 py-2 text-left font-bold text-gray-800 border-x border-y"
                    >
                      {header}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.length > 0 ? (
                  rows.map((row, rIndex) => (
                    <TableRow key={rIndex} className="hover:bg-gray-50">
                      {row.map((cell, cIndex) => (
                        <TableCell
                          key={cIndex}
                          className={`px-4 py-2 text-left border-x border-y ${
                            cIndex === 0 ? 'pl-4' : ''
                          }`}
                        >
                          {cell}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={headers.length} className="text-center py-4">
                      Nie wybrano żadnych wierszy.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>

          {/* Textarea pod tabelą */}
          <div className="space-y-2">
            <Label htmlFor="comment">Dodatkowy komentarz</Label>
            <Textarea
              id="comment"
              placeholder="Tutaj możesz dodać komentarz, który trafi do pliku PDF..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={4}
            />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Anuluj
          </Button>
          <Button onClick={handleGeneratePdf} disabled={rows.length === 0}>
            Wygeneruj PDF
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default DialogAddComment;
