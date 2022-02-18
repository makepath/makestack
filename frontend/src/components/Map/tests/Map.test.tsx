import App from "App";
import { render, screen } from "lib/testing-library";
import Layers from "../Layers";


describe('Layer component', () => {
  it('Should check if the layer component is rendered', () => {
    render(<App />);
    const something = screen.getByRole("main")
    expect(something).toBeInTheDocument()
  })
})