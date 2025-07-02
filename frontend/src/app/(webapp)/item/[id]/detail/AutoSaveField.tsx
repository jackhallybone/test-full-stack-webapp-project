'use client';

import React, { useState } from 'react';
import { cn } from '@/app/lib/utils';

type SaveState = 'idle' | 'editing' | 'saving' | 'saved' | 'error';

type AutoSaveFieldProps = {
  id: string;
  label: string;
  initialValue: string;
  type?: 'input' | 'textarea';
  onSave: (newValue: string) => Promise<void>;
};

export function AutoSaveField({
  id,
  label,
  initialValue,
  type = 'input',
  onSave,
}: AutoSaveFieldProps) {
  const [value, setValue] = useState(initialValue);
  const [saveState, setSaveState] = useState<SaveState>('idle');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setValue(e.target.value);
    setSaveState('editing');
  };

  const handleSave = async () => {
    if (saveState === 'idle') return;

    setSaveState('saving');
    try {
      await onSave(value);
      setSaveState('saved');
      setTimeout(() => setSaveState('idle'), 2000);
    } catch (err) {
      console.error('Save failed:', err);
      setSaveState('error');
    }
  };

  const SaveStateClass = {
    idle: 'border-foreground',
    editing: 'border-foreground',
    saving: 'border-brand-blue',
    saved: 'border-brand-green',
    error: 'border-brand-red',
  }[saveState];

  const commonProps = {
    id,
    value,
    onChange: handleChange,
    onBlur: handleSave,
    className: cn(
      'border-2 rounded px-3 py-2 w-full transition-colors duration-300 focus:outline-none focus:ring-1 focus:ring-foreground',
      SaveStateClass
    ),
  };

  return (
    <form className="space-y-6 max-w-xl" onSubmit={e => e.preventDefault()}>
      <label htmlFor={id} className="block mb-1 font-semibold">{label}</label>
      {type === 'textarea' ? (
        <textarea {...commonProps} />
      ) : (
        <input type="text" {...commonProps} />
      )}
    </form>
  );
}
