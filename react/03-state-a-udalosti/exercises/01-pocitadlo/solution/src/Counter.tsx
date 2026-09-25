import { type ChangeEvent, useState } from "react";

interface CounterProps {
  step?: number;
}

export function Counter(props: CounterProps) {
  const [count, setCount] = useState<number>(() => 0);
  const [step, setStep] = useState(props.step ?? 1);

  const increment = () => {
    setCount((count) => count + step);
  };

  const decrement = () => {
    setCount((count) => count - step);
  };

  const reset = () => {
    setCount(0);
  };

  const handleStepChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.valueAsNumber;
    setStep(() => isNaN(value) ? 0 : value);
  };


  return (
    <div>
      <div>Counter: { count }</div>
      <div>
        <button onClick={ increment }>increment +</button>
        <button onClick={ decrement }>decrement -</button>
        <button onClick={ reset }>reset</button>
      </div>
      <div>
        <div>Step: <input type="number" value={ step } onChange={ handleStepChange } /></div>
      </div>
    </div>
  );
}