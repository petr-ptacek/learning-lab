import { useState, type ChangeEvent } from 'react'

export function CounterWithStep() {
  const [count, setCount] = useState(0)
  const [step, setStep] = useState(1)

  function handleStepChange(e: ChangeEvent<HTMLInputElement>) {
    setStep(e.target.valueAsNumber)
  }

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount((c) => c + step)}>+krok</button>
      <button onClick={() => setCount((c) => c - step)}>-krok</button>
      <button onClick={() => setCount(0)}>Reset</button>
      <label>
        Krok: <input type="number" value={step} onChange={handleStepChange} />
      </label>
    </div>
  )
}
