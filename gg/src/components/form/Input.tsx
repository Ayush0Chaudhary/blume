import { _INPUT_PROPS } from '@/types';
import { useId } from 'react';

const Input = ({ name, placeholder, type, isRequired, label, errorMessage }: _INPUT_PROPS) => {
  const id = useId();
  return (
    <div className='w-max flex flex-col gap-10 px-2'>
      <label htmlFor={id} className='text-3xl'>
        {label}
        {isRequired && <span className='text-red-500'>*</span>}
      </label>
      <input
        className='focus:border-black outline-none border-gray-600 border-2 rounded-xl sm:text-2xl placeholder:flex placeholder:flex-row placeholder:justify-between p-2 text-sm text-black'
        name={name}
        id={id}
        placeholder={placeholder}
        type={type}
        required={isRequired}
      />
      {errorMessage != null ? <div className='text-red-500  font-ligh'>{errorMessage}</div> : ''}
    </div>
  );
};

export default Input;
