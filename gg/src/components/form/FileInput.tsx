import { _FILE_INPUT_PROPS } from '@/types';
import { useId } from 'react';

const FileInput = ({ isRequired, accept, label, errorMessage }: _FILE_INPUT_PROPS) => {
  const id = useId();
  return (
    <div className='flex flex-col gap-10  px-2 w-max'>
      <label htmlFor={id} className='text-3xl flex flex-row'>
        {label} {isRequired && <span className='text-red-500'>*</span>}
      </label>
      <input
        type='file'
        required={isRequired}
        id={id}
        accept={accept}
        className='w-full text-sm text-black-500
      file:mr-4 file:px-3 file:py-1
      file:rounded-3xl file:border-0
      file:text-lg file:font-semibold
      file:bg-black file:text-white
      hover:file:bg-gray-400'
      />
      {errorMessage != null ? <div className='text-red-500  font-ligh'>{errorMessage}</div> : ''}
    </div>
  );
};

export default FileInput;
