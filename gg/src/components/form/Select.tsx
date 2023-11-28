import { _SELECT_PROPS } from '@/types';
import { useId } from 'react';

const Select = ({ name, options, label, isRequired, errorMessage }: _SELECT_PROPS) => {
  const id = useId();
  return (
    <div className='w-max flex flex-col px-2 gap-10'>
      <label htmlFor={id} className='text-3xl'>
        {label}
        {isRequired ? <span className='text-red-500'>*</span> : ''}
      </label>
      <select
        name={name}
        id={id}
        className='border-gray-400 border-2 p-3 rounded-xl bg-white'
        required={isRequired}
      >
        {options.map((option) => {
          return (
            <option key={options.indexOf(option)} value={option}>
              {option}
            </option>
          );
        })}
      </select>
      {errorMessage != null ? <div className='text-red-500  font-ligh'>{errorMessage}</div> : ''}
    </div>
  );
};

export default Select;
