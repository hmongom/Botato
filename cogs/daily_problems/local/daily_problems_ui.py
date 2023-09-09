#  * @copyright   This file is part of the "Botato" project.
#  * 
#  *              Every file is free software: you can redistribute it and/or modify
#  *              it under the terms of the GNU General Public License as published by
#  *              the Free Software Foundation, either version 3 of the License, or
#  *              (at your option) any later version.
#  * 
#  *              These files are distributed in the hope that they will be useful,
#  *              but WITHOUT ANY WARRANTY; without even the implied warranty of
#  *              MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  *              GNU General Public License for more details.
#  * 
#  *              You should have received a copy of the GNU General Public License
#  *              along with the "Botato" project. If not, see <http://www.gnu.org/licenses/>.


import asyncio
import discord


class ProblemSelect(discord.ui.Select):
  def __init__(self, user_id: int, problems: list[dict], future: asyncio.Future, 
              *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.user_id = user_id
    for i, problem in enumerate(problems):
      self.add_option(label = f"{i + 1}. {problem['category']}", value = i)
    self.future = future

  async def callback(self, interaction: discord.Interaction) -> None:
    if interaction.user.id != self.user_id:
      return # User not authorized
    await interaction.response.defer()
    choice = int(self.values[0])
    self.future.set_result(choice)


class FutureIdButton(discord.ui.Button):
  def __init__(self, user_id: int, future: asyncio.Future, id: int, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.user_id = user_id
    self.future = future
    self.id = id

  async def callback(self, interaction: discord.Interaction) -> None:
    if interaction.user.id != self.user_id:
      return # User not authorized
    await interaction.response.defer()
    self.future.set_result(self.id)


class FutureModalButton(discord.ui.Button):
  def __init__(self, future: asyncio.Future, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.future = future

  async def callback(self, interaction: discord.Interaction) -> None:
    future_response = asyncio.Future()
    option_modal = FutureModal(future = future_response, title = "Set an option for your problem", 
                              label = "Option", placeholder = "option")
    await interaction.response.send_modal(option_modal)
    response = await future_response
    self.future.set_result(response)


class FutureModal(discord.ui.Modal):
  def __init__(self, future: asyncio.Future, label: str, placeholder: str, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.add_item(discord.ui.TextInput(label = label, placeholder = placeholder))
    self.future = future

  async def on_submit(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer()
    value = str(self.children[0])
    self.future.set_result(value)


class SolutionSelect(discord.ui.Select):
  def __init__(self, future: asyncio.Future, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.options = [
      discord.SelectOption(label = "Option 0", value = 0),
      discord.SelectOption(label = "Option 1", value = 1),
      discord.SelectOption(label = "Option 2", value = 2),
      discord.SelectOption(label = "Option 3", value = 3)
    ]
    self.placeholder = "Set Solution"
    self.future = future
  
  async def callback(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer()
    result = int(self.values[0])
    self.future.set_result(result)