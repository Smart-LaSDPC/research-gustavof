package air_conditioner

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"
	"uty-api/internal/common/constant"
	errors "uty-api/internal/common/error"

	"github.com/gin-gonic/gin"
	"gopkg.in/go-playground/validator.v9"
)

type Handler struct {
	Validate     *validator.Validate
	ACRepository ACRepository
}

func NewHandler(r *gin.Engine, route string, val *validator.Validate, acRepo ACRepository) {
	handler := &Handler{
		Validate:     val,
		ACRepository: acRepo,
	}
	v1 := r.Group(route)
	{
		v1.GET("", handler.GetAll)
		v1.GET("/create_table", handler.CreateTable) // Route to create the table
		v1.GET("/create", handler.SaveMany)          // eg. localhost:8080/iot/create?n=500
	}
}

// Handler for creating the database table
func (h *Handler) CreateTable(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), constant.CTX_DEFAULT*time.Second)
	defer cancel()

	// Call the repository function to create the table
	err := h.ACRepository.CreateTable(ctx)
	if err != nil {
		c.JSON(http.StatusInternalServerError, errors.Response{
			Status:  http.StatusInternalServerError,
			Type:    constant.ErrDatabaseOperation,
			Message: []string{"Error creating the table", err.Error()},
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"Status":  http.StatusOK,
		"Message": "Table created successfully or already exists",
	})
}

func (h *Handler) GetAll(c *gin.Context) {
	ctx := context.Background()

	limit := c.Query("limit")
	offset := c.Query("offset")

	podName := os.Getenv("POD_NAME")
	nodeName := os.Getenv("NODE_NAME")
	c.Header("X-Pod-Name", podName)
	c.Header("X-Node-Name", nodeName)

	result, err := h.ACRepository.GetAll(ctx, limit, offset)
	if err != nil {
		// Add each to the response headers
		c.JSON(http.StatusNotFound, errors.Response{
			Status:   http.StatusNotFound,
			Type:     constant.ErrUnknownResource,
			PodName:  podName,
			NodeName: nodeName,
			Message:  []string{err.Error()}})
	} else {
		c.JSON(http.StatusOK, gin.H{
			"pod_name":  podName,
			"node_name": nodeName,
			"result":    result,
		})
	}
}

func (h *Handler) SaveMany(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), constant.CTX_DEFAULT*time.Second)
	defer cancel()

	amount := c.Query("n")
	if amount == "" {
		amount = "100"
	}
	amountInt, _ := strconv.Atoi(amount)
	acColl := createRandomACSensorCollection(amountInt)

	count, err := h.ACRepository.SaveMany(ctx, acColl)
	if err != nil {
		c.JSON(http.StatusBadRequest, errors.Response{
			Status:  http.StatusBadRequest,
			Type:    constant.ErrDatabaseOperation,
			Message: []string{err.Error()}})
		return
	}
	msg := fmt.Sprintf("Created %v Air Conditioner records successfully", count)
	c.JSON(http.StatusCreated, gin.H{
		"Status":  http.StatusCreated,
		"Message": msg,
	})
}
