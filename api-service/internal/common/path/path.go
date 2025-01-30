package path

import (
	"os"
	"regexp"

	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
)

const projectDirName = "extractor-kafka"

// LoadEnv loads env vars from .env
func LoadEnv() error {
	rootPath, cwd, err := GetRootPath()
	if err != nil {
		return err
	}
	//if conf.Environment != "QA" && conf.Environment != "" {
	err = godotenv.Load(string(rootPath) + `/.env`)
	if err != nil {
		log.Printf("Problem loading .env file")
		log.Printf("cause %s \n cwd %s", err.Error(), cwd)
	}
	//}
	return nil
}

func GetKeyPath(suffix string) (string, string, error) {
	rootPath, cwd, err := GetRootPath()
	if err != nil {
		return "", cwd, err
	}
	path := string(rootPath) + "/internal/seal/keys/" + suffix
	return path, cwd, nil
}

func GetRootPath() ([]byte, string, error) {
	re := regexp.MustCompile(`^(.*` + projectDirName + `)`)
	cwd, err := os.Getwd()
	if err != nil {
		return nil, "", err
	}
	rootPath := re.Find([]byte(cwd))
	return rootPath, cwd, nil
}
