import { _CHECKBOX_PROPS } from '@/types';
import { useId } from 'react';

const Checkbox = ({ name, value, label, isRequired, default_value, errorMessage }: _CHECKBOX_PROPS) => {
  const id = useId();
  return (
    <div className='flex flex-row px-2 gap-5 items-center w-max'>
      <input
        type='checkbox'
        name={name}
        id={id}
        className='w-5 h-5'
        value={value}
        defaultChecked={default_value}
        required={isRequired}
      />
      <label htmlFor={id} className='text-3xl'>
        {label}
        {isRequired && <span className='text-red-500'>*</span>}
      </label>
      {errorMessage != null ? <div className='text-red-400 text-2xl font-light'>{errorMessage}</div> : ''}
    </div>
  );
};

export default Checkbox;
