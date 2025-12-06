import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Link } from 'react-router-dom';

import * as yup from 'yup';
import { useState } from 'react';
import { Formik, Field, Form } from 'formik';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { useAppDispatch } from '@/store/hooks';
import { setUserProfile } from '@/store/userState';

function LoginForm({ className, ...props }: React.ComponentProps<'form'>) {
  const [loginError, setLoginError] = useState('');
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const validationSchema = yup.object({
    email: yup.string().trim().required('Podaj swój e-mail').email('Nieprawidłowy adres e-mail'),
    password: yup.string().required('Podaj hasło'),
  });

  return (
    <>
      <Formik
        initialValues={{ email: '', password: '' }}
        validationSchema={validationSchema}
        validateOnBlur
        validateOnChange={false}
        onSubmit={async (values) => {
          try {
            const res = await fetch(`/api/user/login`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              credentials: 'include',
              body: JSON.stringify(values),
            });

            const data = await res.json().catch(() => null);
            if (!res.ok) {
              setLoginError(data?.detail ?? 'Błędny login lub hasło.');
              return;
            }

            if (data?.success) {
              dispatch(
                setUserProfile({
                  userId: data.clientId,
                  userEmail: data.email,
                  userName: data.name,
                  userSurname: data.surname,
                })
              );
            }
            setLoginError('');
            if (data.role === 'admin') {
              navigate('/admin');
            } else {
              navigate('/admin');
            }
          } catch (err) {
            setLoginError('Przeraszamy wystąpił błąd serera');
          }
        }}
      >
        {({}) => (
          <Form noValidate className={cn('flex flex-col gap-6', className)} {...props}>
            <div className="flex flex-col items-center gap-2 text-center">
              <h1 className="text-2xl font-bold">Zaloguj się</h1>
              <p className="text-muted-foreground text-sm text-balance">
                Wprowadź poniżej swoją nazwę użytkonika i hasło
              </p>
            </div>
            <div className="grid gap-1">
              <div className="grid gap-3">
                <Field name="email">
                  {({ field, meta }: any) => (
                    <div className="grid gap-2">
                      <Label htmlFor="email">Nazwa użytkonika</Label>
                      <Input
                        id="text"
                        type="text"
                        placeholder="jan.kowalski"
                        {...field}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                        }}
                      />
                      <p
                        className={`text-xs text-center ${meta.touched && meta.error ? 'text-red-500' : 'invisible'}`}
                        aria-live="polite"
                        id="email-error"
                      >
                        {meta.error || 'placeholder'}
                      </p>
                    </div>
                  )}
                </Field>
              </div>
              <div className="grid gap-3">
                <Field name="password">
                  {({ field, meta }: any) => (
                    <div className="grid gap-2">
                      <Label htmlFor="password">Hasło</Label>
                      <Input
                        id="password"
                        type="password"
                        placeholder="*******"
                        {...field}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
                        }}
                      />
                      <p
                        className={`text-xs text-center ${meta.touched && meta.error ? 'text-red-500' : 'invisible'}`}
                        aria-live="polite"
                        id="email-error"
                      >
                        {meta.error || 'placeholder'}
                      </p>
                    </div>
                  )}
                </Field>
              </div>
              <div className={'pt-3'}>
                <Button type="submit" className="w-full">
                  Zaloguj się
                </Button>
                <p
                  className={`text-xs text-center pt-2 ${loginError ? 'text-red-500' : 'invisible'}`}
                  aria-live="polite"
                  id="email-error"
                >
                  {loginError || 'placeholder'}
                </p>
              </div>
            </div>
            <div className="text-center text-sm">
              <a href="#" className="underline underline-offset-4">
                Zapomniałeś hasła?
              </a>
            </div>
          </Form>
        )}
      </Formik>
    </>
  );
}
export default LoginForm;
