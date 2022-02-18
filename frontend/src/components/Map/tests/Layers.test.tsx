import { render } from "lib/testing-library";
import { server } from "mocks/server";
import { useSelector } from "react-redux";
import { getLayersService } from "services/layers";
import IStore from "lib/redux/models";
import { ILayersState } from "storage/layers/models";
import Home from "views/Home";
import Layers from "../Layers";

describe('Layer component', () => {
  it('Should check if the layer component is rendered', async () => {
    const container = render(<Home />)
    expect(container.getByRole('main')).toBeInTheDocument()
    expect(await container.findByText('Regions', undefined, {timeout: 4000})).toBeInTheDocument()
  })
})