# Escort Task Example

Demonstrates the use of the `Escort` task. First, a complex ground route is generated for a ground vehicle in the system. Subsequently, three `Escort` tasks are created: two for ground vehicles that will lead and lag the VIP and a third for an aircraft directly overhead.

This example shows a bug in task creation when large routes exist on current vehicles in the system (`36d9c4793c0b11ce05b3d40ac1e2171af4ec013c` commit in OpenUxAS)
