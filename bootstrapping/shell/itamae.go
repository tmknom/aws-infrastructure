package shell

import (
	. "../role"
	"fmt"
	"os/exec"
)

type Itamae struct {
	Role      Role
	IpAddress string
}

func (i Itamae) Execute() {
	fmt.Println("Provisioning with itamae: " + i.Role)
	cmd := exec.Command("fab", "itamae_"+i.Role.String(), "-H", i.IpAddress)
	Shell{}.cdConfigurationPath()
	Shell{Command: *cmd}.executeCommand()
}
