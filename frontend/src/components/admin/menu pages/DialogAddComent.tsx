import { Button } from '@/components/ui/button';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import DatePicker from './DatePicker';


type RegisterDialogProps = {
  open: boolean;
  onOpenChange: (v: boolean) => void;
};

function DialogAddComment({ open, onOpenChange}: RegisterDialogProps) {


  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Wygeneruj plik PDF z uwagami</DialogTitle>
          <DialogContent>
            <DatePicker></DatePicker>
          </DialogContent>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
}

export default DialogAddComment;
